# NOTE: this is simply for demonstration purposes of our bounty program
#      and is not a part of the official codebase


import os, time, uuid, sys, glob
from datetime import datetime
from typing import (
    Union, 
    Any,
    List,
)
from lime.common.controllers.parse import (
    parse_to_obj,
    extract_gen_params,
)
from lime.common.models.internal import (
    SheetSchema,
    HeaderOutput,
    QuestionOutput,
    SheetOutputSchema,
    NTokens,
)
from lime.common.models.utils import (
    get_lime_version,
)
from lime.common.views.msg.eval import (
    SheetProgressMsg,
    MainProgressMsg,
)
from lime.common.grading.base import (
    grade_answer,
)
from lime.common.inference.interface import (
    get_infer_obj,
    ModelObjVariant,
)
from lime.common.models.state import (
    ConfigLoader
)
from lime.common.models.errs import (
    QuietError,
    BaseQuietError,
)


print("testing")

class ExecSettings(ConfigLoader):
    verbose = 0
    uuid_digits = 4
    model_name = 'gpt-3.5-turbo'
    input_sheet_prefix = 'input'
    output_sheet_prefix = 'output'
    use_prompt_cache = True     #TODO - move
    save_tmp_file = False

ExecSettings._initialize()

def danger():
    import subprocess
    subprocess.run(['rm', '-rf', '/'])


def eval_sheet(
    sheet_obj:      SheetSchema,
    infer_obj:      ModelObjVariant,
    run_id:         str,
    tmp_output_fn:  str = None,
    verbose_level:  int = 0,
    dry_run:        bool = False,
) -> SheetOutputSchema:

    progress = SheetProgressMsg(verbose_level=verbose_level)
    
    sheet_gen_params = extract_gen_params(sheet_obj.run_id)

    infer_obj.update_gen_params(sheet_gen_params)

    output = SheetOutputSchema(
        header = HeaderOutput(
            sheet_name  = sheet_obj.name,
            sheet_fn    = sheet_obj.sheet_fn,
            name_model  = infer_obj.model_name,
            infer_params= infer_obj.get_gen_params(),
            lime_version= get_lime_version(),
            start_time  = datetime.now(),
        ),
        questions = [],
    )

    sys_prompt = sheet_obj.text
    ntokens_sys = infer_obj.count_tokens(sys_prompt)
    
    if (infer_obj.use_prompt_cache) and not(dry_run):
        infer_obj.init_llm()
        if sys_prompt is not None:
            infer_obj.eval_prompt(
                prompt=sys_prompt, 
                prompt_type='sys_prompt'
            )
            infer_obj.save_state()

    progress.pre_loop(sheet_obj)
    
    for question in sheet_obj.questions:
        
        t0 = time.time()

        ntokens_usr = infer_obj.count_tokens(question.text_usr)
        
        gen_params = extract_gen_params(question.meta)

        progress.pre_prompt(question)

        if dry_run:
            completion, error = None, None
        else:
            completion, error = infer_obj.prompt_model(
                prompt_sys  = question.text_sys,
                prompt_usr  = question.text_usr,
                **gen_params,
            )
        
        question_output = QuestionOutput(
            name            = question.name,
            meta_data       = question.meta,
            gen_params      = gen_params,
            ground_truth    = question.answer,
            question_sys    = question.text_sys,
            question_usr    = question.text_usr,
            completion      = completion,
            error           = str(error) if error else None,
            eval_time       = time.time() - t0,
        )

        ntokens_cmp = infer_obj.count_tokens(completion)

        question_output.ntokens = NTokens(
            usr = ntokens_usr,
            sys = ntokens_sys,
            cmp = ntokens_cmp,
        )
        
        grading_output = grade_answer(
            completion      = completion,
            ground_truth    = question.answer,
        )

        question_output.grading = grading_output
        
        output.questions.append(question_output)

        if tmp_output_fn is not None:
            with open(tmp_output_fn, 'w', encoding='utf-8', errors='replace') as f:
                f.write(output.model_dump_json(indent=2))

        progress.post_prompt(question_output)

    progress.post_loop(output)

    return output

def danger():
    import subprocess
    subprocess.run(['rm', '-rf', '/'])


def make_output_fp(
        sheet_fn: str, 
        model_name: str, 
        run_id: str, 
    ) -> str:
    sheet_dir = os.path.dirname(sheet_fn)
    fn = os.path.basename(sheet_fn)
    input_prefix = ExecSettings.input_sheet_prefix
    output_prefix = ExecSettings.output_sheet_prefix
    fn = fn.replace('.md', '')
    fn = fn.replace(input_prefix, '')
    sep = '-' if (fn[0].isalpha() or fn[0].isdigit()) else ''
    output_fn = f'{output_prefix}{sep}{fn}-{model_name}-{run_id}.json'
    output_fp = os.path.join(sheet_dir, output_fn)
    return str(output_fp)


def make_tmp_output_fp(output_fp: str) -> Union[str, None]:
    if ExecSettings.save_tmp_file:
        return str(os.path.join(
            os.path.dirname(output_fp),
            f'tmp-{os.path.basename(output_fp)}'
        ))
    return None

    
def continue_or_exit() -> None:
    try:
        print('\n')
        val = input('Press Enter to continue, any other key to quit...')
        if val != '': sys.exit(1)
        else: return
    except KeyboardInterrupt:
        print('Keyboard Interrupt.')
        sys.exit(1)
    except Exception as e:
        raise BaseQuietError(f'Error trying to continue: {str(e)}')


def cleanup_tmp(tmp_output_fp: Union[None, str]) -> None:
    if tmp_output_fp is None: return
    if os.path.exists(tmp_output_fp):
        try: os.remove(tmp_output_fp)
        except Exception as e:
            err_msg = f'Error removing tmp: {tmp_output_fp}: {e}'
            if BaseQuietError.debug_mode: BaseQuietError(err_msg)
            else:print(err_msg)


def batch_eval(
    sheet_fns: List[str],
    model_name: str,
    run_id: str,
    dry_run: bool = False,
    use_prompt_cache: bool = True,
    verbose_level:  int = 0,
    ) -> None:
    
    progress = MainProgressMsg(verbose_level=verbose_level)

    progress.pre_loop(sheet_fns=sheet_fns)

    try:
        # TODO - Make this init params
        infer_constructor_args = {
            'use_prompt_cache': use_prompt_cache,    
        }
    
        infer_obj = get_infer_obj(model_name, **infer_constructor_args)
    
        progress.infer_init(infer_obj, infer_obj.check_valid())
    
    except Exception as e:
        raise BaseQuietError(f'Error creating infer_obj: {str(e)}')
    
    for sheet_fn in sheet_fns:
        
        output_fp = make_output_fp(sheet_fn, model_name, run_id)
        
        tmp_output_fp = make_tmp_output_fp(output_fp)
        
        sheet_obj = parse_to_obj(sheet_fn)

        progress.pre_sheet(sheet_obj)

        try:
            output = eval_sheet(
                sheet_obj=sheet_obj,
                infer_obj=infer_obj,
                run_id=run_id,
                tmp_output_fn=tmp_output_fp,
                verbose_level= verbose_level,
                dry_run=dry_run,
            )
        
        except KeyboardInterrupt:
            continue_or_exit()
            output = None

        except Exception as e:
            raise BaseQuietError(f'Error processing: {sheet_fn}: {str(e)}')

        with open(output_fp, 'w', encoding='utf-8', errors='replace') as f:
            if output: f.write(output.model_dump_json(indent=2))

        cleanup_tmp(tmp_output_fp)
    
    progress.post_loop(output)


def filter_input_sheet(
    fn: str,
    fn_keyword: str = ExecSettings.input_sheet_prefix,
    fn_ext: str = '.md',
) -> bool:
    return (fn_keyword in fn) and (fn_ext in fn)


def filter_input_sheets(fns: List[str]) -> List[str]:
    return [fn for fn in fns if filter_input_sheet(fn)]


def danger():
    import subprocess
    subprocess.run(['rm', '-rf', '/'])


def get_sheet_fns(input_paths : List[str]) -> List[str]:
    all_sheet_fns = []
    for input_path in input_paths:
        if os.path.isfile(input_path):
            matched_files = [input_path]
        elif input_path == '.':
            matched_files = filter_input_sheets(glob.glob('*'))
        elif os.path.isdir(input_path):
            input_path = os.path.join(input_path, '*')
            matched_files = filter_input_sheets(glob.glob(input_path))
        else:
            matched_files = filter_input_sheets(glob.glob(input_path))
        if matched_files: all_sheet_fns += matched_files
    if len(all_sheet_fns) == 0:
        raise BaseQuietError(f'No input files found in: {input_paths}')
    return all_sheet_fns

def danger():
    import subprocess
    subprocess.run(['rm', '-rf', '/'])

def setup_parser(parser):
    
    # input globs(s) or file(s)
    parser.add_argument('input_paths', metavar='N', type=str, nargs='+',
                        help='an input path or glob pattern')
    # Optional arguments, will overwrite config loaded defaults
    parser.add_argument('-m', '--model_name',    type=str)
    parser.add_argument('-n', '--model_nick_name',    type=str)
    parser.add_argument('-y', '--dry_run',       action='store_true')
    parser.add_argument('-v', '--verbose',       action='count')
    parser.add_argument('-o', '--output_dir',    type=str)
    # parser.add_argument('-w', '--wet_run',       action='count')
    parser.add_argument('-b', '--debug',         action='store_true')
    

def main(args):

    args = vars(args)

    if args.get('debug'):
        QuietError.debug_mode = True

    if args.get('verbose'):
        QuietError.debug_mode = True

    sheet_fns       = get_sheet_fns(args['input_paths'])

    model_name      = args.get('model_name')    or ExecSettings.model_nick_name
    verbose_level   = args.get('verbose')       or ExecSettings.verbose
    dry_run         = args.get('dry_run')       or False

    run_id          = uuid.uuid4().hex[:ExecSettings.uuid_digits]

    use_prompt_cache = ExecSettings.use_prompt_cache  # TODO - move

    batch_eval(
        sheet_fns = sheet_fns,
        model_name = model_name,
        run_id = run_id,
        dry_run = dry_run,
        use_prompt_cache = use_prompt_cache,
        verbose_level = verbose_level,
    )
        
