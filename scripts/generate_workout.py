#!/usr/local/bin/env python3

import argparse
import jinja2
import os

from jinja2 import Template
from pprint import pprint

# For now this is going to have to be interactive-mode only
# Better inputs to come.


def redundancy_chk(src_path):
    if os.path.exists(src_path):
        confirm = input("\'%s\' exists. Would you like to "
                        "overwrite? [y\\N]: " % src_path)
        if confirm not in ('y', 'Y'):
            new_name = input('New file name: ')
            src_path = "./src/workouts/%s.tex" % new_name
    return src_path


def file_sanitize(name):
    if ' ' in name:
        name = name.replace(' ', '_').lower()
    return name


def write_latex(name, output_dir, content):    
    file_name = '%s/%s.tex' % (output_dir, file_sanitize(name))
    src_file = redundancy_chk(file_name)
    with open(src_file, 'w+') as outfile:
        outfile.write(content)
    return src_file


def get_exercise():
    # *vomiting noises*
    # Building this to return a dict even though it's less efficient in
    # the short term so I can load dicts in from file later and never talk
    # to anyone ever again.
    # TODO: build "superset" template & functionality
    name = input('Exercise Name: ')
    weight = input('Weight (N/A if none): ')
    reps = input('Reps per Set: ')
    sets = input('Sets: ')
    content = {
        'name': name,
        'weight': weight,
        'reps': reps,
        'sets': sets
    }
    pprint(content)
    confirm = input('Does this look correct? [y/N]: ')
    if confirm in ('y', 'Y'):
        return content


def generate_workout(env, length):
    workout_body = ''
    for exercise in range(length):
        content = get_exercise()
        template = env.get_template('./src/templates/single_exercise.tex')
        workout_body += template.render(name=content['name'],
                                        weight=content['weight'],
                                        reps=content['reps'],
                                        sets=content['sets'])

    return workout_body


def main():
    parser = \
        argparse.ArgumentParser(description='Dynamic LaTeX zine template '
                                            'generation tool')
    parser.add_argument('-l', '--length', required='true', type=int,
                        help='Number of exercises to be included in this'
                             'workout')
    parser.add_argument('-t', '--type', required='true', type=str,
                        help='Type of workout (for header)')
    parser.add_argument('-o', '--output', type=str,
                        default='./src/workouts',
                        help='Output directory for your LaTeX src result')
    
    # parser.add_argument('--silent', action='store_true', dest='silent',
    #                     help='Do not output resulting LaTeX to screen')
    # parser.add_argument('--dry-run', action='store_true', dest='dry',
    #                     help='Run without compiling')
    # TODO: Allow for date range input for bulk planning
    # TODO: non-interactive inputs. If I wanted to talk to someone when
    #       planning workouts i'd be working with a trainer.
    # parser.add_argument('--canned', type=str,
    #                    help='Path to static file to be used in-lieu of'
    #                         'interactive input')
    args = parser.parse_args()

    latex_jinja_env = jinja2.Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    workout_body = generate_workout(latex_jinja_env, args.length)
    workout_template = latex_jinja_env.get_template(
        './src/templates/workout_wrapper.tex')
    full_workout = workout_template.render(workoutType=args.type,
                                           workoutContent=workout_body)
    # if not args.silent:
        # switch this later for something useful
    #    os.system('clear')
    #    print(full_workout)

    # Write to file
    src_file = write_latex(args.type, args.output, full_workout)
    print("Output found at %s" % src_file )
    print()

    # if not args.dry:
    # TODO: compile latex and move resulting file to the forms/workouts dir


main()
