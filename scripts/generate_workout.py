#!/usr/local/bin/env python3

import argparse
import jinja2
import os

from jinja2 import Template
from pprint import pprint

# For now this is going to have to be interactive-mode only
# Better inputs to come.


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
    confirm = input('Does this look correct? [y/n]:')
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
    # parser.add_argument('--to-screen', action='store_true', dest='to_screen',
    #                    help='Output resulting LaTeX to screen instead of to '
    #                         'a file in the src/workouts directory')
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
    print()
    print(full_workout)

    # if not args.dry:
    # TODO: compile latex and move resulting file to the forms/workouts dir
main()