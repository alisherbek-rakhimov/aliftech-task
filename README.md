# aliftech-task

**Note:** As I was asked to use `starlette.io`, so decided not to use any other external(ex. validation) package such
as `pydantic`, please, try not to provide suspicious input data, I did not write validation for every possible case
except some basic ones. There is no redirect when doing `POST` to `/contacts` so that it is a test task. **But** I
decided to use Tortoise orm instead of writing raw SQLs for each endpoint

###### Provide input in body as a raw data json format

Please, keep in mind: maybe it is not the best possible way to design the architecture of project but for test-task
purposes I thought it was enough

_input sample_:
`{
"name":"alisher",
"phone":3453983 }`