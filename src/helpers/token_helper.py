'Helpers for token related management'

import logging
from typing import Dict

from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

from config.queries import Queries
from config.string_constants import TokenInfo
from database.database_access import DatabaseAccess

logger = logging.getLogger(__name__)


class TokenHelper:
    'Helper class for token management'

    def __init__(self, database: DatabaseAccess) -> None:
        self.db = database

    def generate_token_data(self, identity: str, mapped_role: str, is_fresh: bool) -> Dict:
        '''Generate token data containing access and refresh tokens'''

        self.revoke_token(user_id=identity)

        access_token = create_access_token(
            identity=identity,
            fresh=is_fresh,
            additional_claims={'cap': mapped_role}
        )
        refresh_token = create_refresh_token(
            identity=identity,
            additional_claims={'cap': mapped_role}
        )
        access_token_jti = get_jti(access_token)
        refresh_token_jti = get_jti(refresh_token)
        self.db.write(Queries.INSERT_TOKEN_DATA, (identity, access_token_jti, refresh_token_jti))

        token_data = {'access_token': access_token, 'refresh_token': refresh_token}
        return token_data

    def revoke_token(self, user_id: str) -> None:
        'Sets the status of token to revoked'

        self.db.write(Queries.UPDATE_TOKEN_STATUS, (user_id, ))

    def check_token_status(self, token_id: str, token_type: str) -> None:
        'Checks if the token is revoked'

        match token_type:

            case TokenInfo.TYPE_ACCESS:
                status_info = self.db.read(Queries.GET_ACCESS_TOKEN_STATUS, (token_id, ))

            case TokenInfo.TYPE_REFRESH:
                status_info = self.db.read(Queries.GET_REFRESH_TOKEN_STATUS, (token_id, ))

        status = status_info[0].get('status')
        return TokenInfo.status.get(status)
