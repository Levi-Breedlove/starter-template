# AWS Emulator for local integration tests

Use AWS Emulator when the project depends on AWS API behavior that the current
emulator release can exercise. Keep unit tests and existing brownfield test
tools. Adopt emulation where it adds coverage for a specific integration or
failure case. The workflow's setup and ordinary consultation need only the
[standard prerequisites](00-quickstart.md).

## Check the project's operations

1. List the services, API operations, resource behaviors, and error paths the
   application or its local tests rely on. Inspect SDK clients, IaC, test
   fixtures, and relevant delivery scripts.
2. When skill use is allowed, discover the official emulator skill through AWS
   Core and retrieve its exact returned identifier. Use its compatibility
   procedure and the current release's operation-level fidelity evidence. Use
   the official project check directly when the skill is unavailable.
   [AWS guidance](02-aws-guidance-and-access.md) · [Project compatibility check](https://docs.aws.amazon.com/emulator/latest/userguide/check-project.html)
3. Mark required behaviors as supported, limited, or unverified and cite the
   evidence. A listed service does not establish every operation, option, or
   failure mode. Exercise unverified behaviors with a scoped local test where
   feasible. Keep checks that depend on AWS enforcement or integration in a
   separately authorized AWS test plan.
4. If emulation fits, record the operations, expected outcomes, selected setup,
   and check commands in the project's design and tasks. Recheck coverage after
   changing the client, API usage, or emulator release.

## Set up an isolated test instance

- On Linux, including suitable Codespaces images, use the official package for
  the architecture. Use the official Docker procedure on macOS or Windows, or
  when Linux or CI uses containers. The Linux package supports 64-bit x86 or Arm with glibc 2.17 or newer. After setup is authorized, follow the platform installation steps, including package verification, and record the observed `aws-emulator -v`.
  [Prerequisites](https://docs.aws.amazon.com/emulator/latest/userguide/setting-up.html) ·
  [Linux installation](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-linux.html) ·
  [Docker setup](https://docs.aws.amazon.com/emulator/latest/userguide/getting-started-docker.html)
- Start a separate instance per test job or environment with synthetic data,
  signing enabled, and a loopback-only endpoint. Choose an unused port. In
  Docker, publish only to loopback. In Codespaces, keep the port unforwarded. Disable telemetry in CI and unattended local
  test processes using `-t off` or the documented container equivalent.
- Connect every client explicitly to the same loopback endpoint and this
  instance's CA and credential files. Keep production profiles, keys, web
  identity, metadata providers, and service-specific endpoint overrides out of
  the test process. For SDK integration tests, set the loopback endpoint and
  verify the endpoint for each client and for any URL passed from a response.
  Restrict test-process egress to the local endpoint where supported.
  [AWS Emulator security](https://docs.aws.amazon.com/emulator/latest/userguide/security.html)

For an already installed Linux instance on an unused default port, start it
with `aws-emulator -p 9297 -t off` in a separate terminal. After it writes its
per-run files, run this synthetic SQS connectivity check with an installed AWS
CLI. The clean command environment excludes inherited credentials, proxy
settings, and endpoint overrides.

```sh
(
  set -eu
  emulator_dir="$HOME/.aws/emulator/9297"
  emulator_url="https://127.0.0.1:9297"
  test -s "$emulator_dir/config"
  test -s "$emulator_dir/emulator_credentials"
  test -s "$emulator_dir/ca.pem"
  curl -q --fail --silent --show-error --max-time 5 --noproxy 127.0.0.1 \
    --cacert "$emulator_dir/ca.pem" "$emulator_url/__admin/health"
  local_aws() {
    env -i PATH="$PATH" AWS_CONFIG_FILE="$emulator_dir/config" \
      AWS_SHARED_CREDENTIALS_FILE="$emulator_dir/emulator_credentials" \
      AWS_EC2_METADATA_DISABLED=true AWS_PAGER= AWS_MAX_ATTEMPTS=1 \
      aws --region us-east-1 --endpoint-url "$emulator_url" \
        --ca-bundle "$emulator_dir/ca.pem" "$@"
  }
  test "$(local_aws sts get-caller-identity --query Account --output text)" = 000000000000
  local_aws sqs list-queues
)
```

A successful test job waits for the local health endpoint and stops its own
instance at teardown. Keep certificate verification enabled. On connection
failure, check the process, bind address, and port. On TLS or signing failure,
check that the test process uses the current instance's CA and generated
credentials. Treat an unsupported operation as a coverage gap and record the
exact operation and release. Stop the test if the endpoint cannot be
established as local. Never commit the generated config, credentials, or CA.

## Record what passed

Retain the emulator and client versions, operations and inputs tested, local
endpoint scope, commands, results, limitations, and the project revision in
the check evidence. This example checks local signing, connectivity and queue listing. Use application-specific assertions for the actual resource behavior and error paths. Real IAM,
KMS policy enforcement, cross-account access, networking, quotas, and deployment
behavior require separately authorized AWS verification.
[AWS Emulator source and releases](https://github.com/aws/aws-emulator)
