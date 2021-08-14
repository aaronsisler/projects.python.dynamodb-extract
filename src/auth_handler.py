def main(event, context):
    # print("Client token: " + event['authorizationToken'])
    print("Starting Auth")
    print("Method ARN: " + event['methodArn'])

    principal_id = "user|a1b2c3d4"

    method_arn = event['methodArn']
    print(method_arn)

    print(event)

    print(event['authorizationToken'])

    if event['authorizationToken'] == 'Bearer allow':
        policy = AuthPolicy(principal_id, method_arn, 'Allow')
    elif event['authorizationToken'] == 'Bearer deny':
        policy = AuthPolicy(principal_id, method_arn, 'Deny')
    else:
        raise Exception('Unauthorized')

    # Finally, build the policy
    return policy.build()


class AuthPolicy(object):
    principal_id = ""
    """The principal used for the policy, this should be a unique identifier for the end user."""
    version = "2012-10-17"
    """The policy version used for the evaluation. This should always be '2012-10-17'"""

    def __init__(self, principal_id, method_arn, effect):
        self.principal_id = principal_id
        self.method_arn = method_arn
        self.effect = effect

    def _getEmptyStatement(self):
        """Returns an empty statement object prepopulated with the correct action and the
        desired effect."""
        statement = {
            'Action': 'execute-api:Invoke',
            'Effect': self.effect,
            'Resource': []
        }

        return statement

    def _getStatementForEffect(self, resource):
        """This function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy."""
        statements = []

        statement = self._getEmptyStatement()
        statement['Resource'].append(resource)

        statements.append(statement)

        return statements

    def build(self):
        policy = {
            'principalId': self.principal_id,
            'policyDocument': {
                'Version': self.version,
                'Statement': []
            }
        }

        policy['policyDocument']['Statement'].extend(self._getStatementForEffect(self.method_arn))

        return policy
