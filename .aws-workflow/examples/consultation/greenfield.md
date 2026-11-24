# Greenfield example: a booking capability

This is a fictional consultation excerpt. No application was built or AWS resource queried. Assume the fictional project's brief already establishes a Python API, authenticated staff and customers, one location, low initial traffic, no payments, and a first release limited to availability and booking. Authentication and data-handling policies are linked existing decisions. The service choices below are an illustrative recommendation, not a bootstrap default.

## 1. Understand the request and lead the interview

**User:** “Plan the booking capability for AWS. Staff publish availability and customers book. Keep operations simple. I want you to recommend the technical approach.”

**Codex:** “The brief gives me the users, Python, AWS, existing identity rules, and the first-release boundary. I recommend a small managed API and durable booking store. API Gateway, Lambda, and DynamoDB are a candidate for this access pattern; I will check the service behavior and cost assumptions before finalizing the design.

“Preventing double bookings means the booking decision must be enforced where the slot is stored. I will also define retries so a network interruption cannot create a second booking. Two product decisions affect that contract:

1. Does selecting an available slot confirm it immediately, or does staff approval come first? I recommend immediate confirmation if published availability is already trusted.
2. Are appointments one fixed duration or different durations by service? Fixed durations let this first release use explicit non-overlapping slots.”

**User:** “Immediate confirmation and thirty-minute slots. Staff should also be able to remove availability.”

The agent records the answers before proceeding. It does not ask the user to choose a database consistency mechanism or repeat the project's language and authentication decisions.

## 2. Let the answer shape the next question

**Codex:** “I have saved immediate confirmation and thirty-minute slots. I am drafting the reservation and retry requirements. Removing availability introduces one policy question: should it affect an existing confirmed booking? I recommend removing the slot from future bookings while preserving any existing confirmation; cancellation can remain separate.”

**User:** “Yes. Removing availability must not cancel bookings. Cancellation is outside the first release.”

The work's requirements record now includes:

| Decision | Actual fictional answer | Consequence |
| --- | --- | --- |
| Q-001 | Confirm immediately. | The durable reservation result determines confirmation. |
| Q-002 | Use thirty-minute slots. | Slot identity and collision checks use fixed intervals. |
| Q-003 | Removing availability preserves confirmations. | Availability changes need an explicit preservation condition. |

The next draft covers successful reservation, competing reservation attempts, retries, unauthorized access, and the availability/confirmed-booking interaction. Region and traffic quantities remain labeled estimate assumptions until established; they are not silently treated as spending or deployment permission.

## 3. Analyze requirements and perform the first review

**Codex:** “The requirement set now distinguishes availability from an existing reservation. I checked the interaction between removing availability, a simultaneous booking, and retrying a completed booking. The contract will require one authoritative result, preserve existing confirmations, and return a defined conflict when another booking wins.

“Here is the first-release scope and its acceptance summary. The implementation will need checks for a successful reservation, two competing customers, a retried request, removed availability, and existing identity rules. Is this the booking behavior you intended?”

**User:** “Yes, that is the intended scope. Choose the technical details and complete the design and task plan. Do not deploy.”

In this fictional session, that answer supplies a real requirements decision and delegates the technical planning choices. The record identifies the reviewed requirements revision and the actual message. It does not authorize deployment. Codex should not ask for another permission merely to write `design.md` or `tasks.md`.

## 4. Develop and review the design

**Codex:** “I recommend API Gateway with a Python Lambda handler and a DynamoDB slot record for this bounded access pattern. The design uses conditional state changes to prevent a competing booking from replacing an existing reservation. It associates the request identity with the stored result and checks ownership before returning a previous result. Availability changes follow the preserved-booking contract.

“I will document API errors, authentication integration, access boundaries, diagnostic signals, recovery assumptions, and the cost model. Local checks can exercise the application contract; actual managed-service concurrency and IAM behavior remain separate integration obligations.”

The service mechanisms need source-backed design, not a name-only architecture. AWS documents [API Gateway's Lambda proxy integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html) and [DynamoDB conditions on writes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html). Those mechanisms support the proposed design; they do not by themselves establish the application's correctness or total cost.

Codex reviews the design against the requirements under the user's delegated technical-planning authority and records its actual findings and outcome. An author design review is recorded as such. It is not called an independent review. Any unresolved product conflict would return to the interview rather than being hidden by a technical choice.

## 5. Produce tasks that follow from the decisions

An illustrative task breakdown is:

| Task | Outcome | Prerequisite | Evidence obligation |
| --- | --- | --- | --- |
| T-001 | Define slot, reservation, retry, and error contracts. | None | Contract examples include competing requests and preserved bookings. |
| T-002 | Implement the scoped booking and availability operations. | T-001 | Local checks cover successful, conflict, retry, and preservation paths. |
| T-003 | Add the scoped infrastructure and identity integration. | T-001 | IaC and local contract checks; account-specific claims remain pending. |
| T-004 | Verify the integrated candidate and review it. | T-002, T-003 | Required checks and actual review evidence for that candidate. |
| T-005 | Prepare operational guidance and the later release procedure. | T-004 | Defined signals, recovery, cost assumptions, and explicit cloud proof obligations. |

The real `tasks.md` would use explicit requirement and check IDs for each row. Codex checks coverage and dependencies, records the planning review, and finishes with the exact next task. All implementation boxes remain unchecked because this example has only planned the work.

**Codex:** “The reviewed planning artifacts are ready for the first local implementation task, T-001. The requirements decision and delegated design review are recorded. Deployment remains outside the current scope, and the AWS integration checks are pending.”

## What this illustrates

The interview discovered three business rules in two small rounds. Engineering consequences came from those answers and the existing brief. The technical recommendation was owned by Codex, the requirements review was real within the fictional dialogue, delegated authority avoided repetitive permissions, and the task plan retained honest evidence boundaries.
