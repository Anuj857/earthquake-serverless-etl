import os
import shutil
import subprocess
import sys

LAMBDAS = [
    {
        "folder": "lambda/fetch_lambda",
        "zip": "fetch_lambda.zip",
        "function": "earthquake-fetch-lambda",
    },
    {
        "folder": "lambda/etl_lambda",
        "zip": "etl_lambda.zip",
        "function": "earthquake-etl-lambda",
    },
]


def deploy_lambda(folder, zip_name, function_name):

    print("=" * 60)
    print(f"Packaging {function_name}")
    print("=" * 60)

    # Remove old zip if it exists
    if os.path.exists(zip_name):
        os.remove(zip_name)

    # Create zip
    shutil.make_archive(
        zip_name.replace(".zip", ""),
        "zip",
        folder
    )

    print(f"{zip_name} created successfully.")

    print("=" * 60)
    print(f"Deploying {function_name}")
    print("=" * 60)

    subprocess.run(
        [
            "aws",
            "lambda",
            "update-function-code",
            "--function-name",
            function_name,
            "--zip-file",
            f"fileb://{zip_name}",
        ],
        check=True,
    )

    print(f"{function_name} deployed successfully.\n")


def main():

    try:

        print("\nStarting Automatic Lambda Deployment\n")

        for item in LAMBDAS:

            deploy_lambda(
                item["folder"],
                item["zip"],
                item["function"],
            )

        print("=" * 60)
        print("ALL DEPLOYMENTS COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except subprocess.CalledProcessError as e:

        print(f"AWS CLI Deployment Failed: {e}")
        sys.exit(1)

    except Exception as e:

        print(f"Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()