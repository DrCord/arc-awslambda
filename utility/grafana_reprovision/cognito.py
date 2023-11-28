import boto3
import getpass


DEFAULT_CLIENT_ID = "5onspj4jo1ors18t8cih8lpn30"


def authenticate(username, client_id=DEFAULT_CLIENT_ID):

    password = getpass.getpass()
    cognito_client = boto3.client('cognito-idp')
    auth_response = cognito_client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    auth_result = auth_response.get("AuthenticationResult", None)
    if auth_result is not None:
        return auth_result.get("IdToken", None)

    challenge = auth_response.get("ChallengeName", None)
    session = auth_response.get("Session", None)
    while challenge is not None:

        if challenge == "NEW_PASSWORD_REQUIRED":
            print("Password reset is required")
            new_password = None
            while new_password is None:
                new_password = getpass.getpass("Enter new password:")
                new_password_verify = getpass.getpass("RE-enter password:")
                if new_password != new_password_verify:
                    new_password = None
                    print("Passwords don't match. Try again.")
            challenge_response = cognito_client.respond_to_auth_challenge(
                ClientId=client_id,
                ChallengeName=challenge,
                ChallengeResponses={
                    "USERNAME": username,
                    "NEW_PASSWORD": new_password
                },
                Session=session
            )
            auth_result = challenge_response.get("AuthenticationResult", None)
            if auth_result is None:
                challenge = challenge_response.get("ChallengeName", None)
                session = challenge_response.get("Session", None)
            else:
                challenge = None

        elif challenge == "SMS_MFA":
            mfa = getpass.getpass("SMS MFA Required:")
            challenge_response = cognito_client.respond_to_auth_challenge(
                ClientId=client_id,
                ChallengeName=challenge,
                ChallengeResponses={
                    "USERNAME": username,
                    "SMS_MFA_CODE": mfa
                },
                Session=session
            )
            auth_result = challenge_response.get("AuthenticationResult", None)
            if auth_result is None:
                challenge = challenge_response.get("ChallengeName", None)
                session = challenge_response.get("Session", None)
            else:
                challenge = None
        elif challenge == "SOFTWARE_TOKEN_MFA":
            mfa = getpass.getpass("SOFTWARE TOKEN MFA Required:")
            challenge_response = cognito_client.respond_to_auth_challenge(
                ClientId=client_id,
                ChallengeName=challenge,
                ChallengeResponses={
                    "USERNAME": username,
                    "SOFTWARE_TOKEN_MFA_CODE": mfa
                },
                Session=session
            )
            auth_result = challenge_response.get("AuthenticationResult", None)
            if auth_result is None:
                challenge = challenge_response.get("ChallengeName", None)
                session = challenge_response.get("Session", None)
            else:
                challenge = None
        else:
            raise Exception(f'Challenge type "{challenge}" not handled!')

    if auth_result is None:
        raise Exception("Failed to authenticate")

    return auth_result.get("IdToken", None)
