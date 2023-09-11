import argparse
import json
import os
from core.test import BaseTest

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=str, required=True)
parser.add_argument("--temperature", type=float, required=False)
parser.add_argument("--top_p", type=float, required=False)
parser.add_argument("--n", type=int, required=False)
parser.add_argument("--max_tokens", type=int, required=False)
parser.add_argument("--param_values", type=str, required=False)
args = parser.parse_args()

test_file = os.path.join(args.test, "test.json")
instances_file = os.path.join(args.test, "instances.json")

test = BaseTest.load_from_file(test_file)

model_args = vars(args).copy()
del model_args["test"]
del model_args["param_values"]
model_args = {k: v for k, v in model_args.items() if v is not None}

param_values = json.loads(args.param_values) if args.param_values is not None else None
for key in param_values:
    assert key not in model_args, f"Parameter {key} clashes with argument {key}."
model_args.update(param_values)

test_instance = test.run(**model_args)

print("Response: ", test_instance.response)

if not test_instance.is_safe:
    choice = input("Instance unsafe. Do you want to add it to the set of instances (y/n)? ")
    if choice == "y":
        with open(instances_file, "a") as fout:
            fout.write(test_instance.model_dump_json() + "\n")
else:
    print("Instance safe, the model is not vulnerable.")

