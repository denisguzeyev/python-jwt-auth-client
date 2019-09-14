JWT auth client
===========================================

 ### Purpose:
 
 Provide easy-to-use interface for JSON web tokens (JWT) validation 
 
 ### Requirements:
 
 Check (verify) whether provided JWT as 'Bearer *token*' is valid and not expired
 
 ### Hints:
 Public key(s) will be automatically obtained accordig to mapped table from jwt_conf.yaml) 
 
 # Important:

 set JWT_CONF_YAML_PATH variable in config file!
 e.g.:
  - JWT_CONF_YAML_PATH = 'jwt_conf.yaml'
    or for yaml format:
  - JWT_CONF_YAML_PATH: jwt.conf.yaml

 Example for jwt_conf.yaml content:
  - zebra_numa: http://localhost:3333/pns/jwk_public/
  where 'zebra_numa' is issuer from JWT and http://localhost:3333/pns/jwk_public/ to get public key_set (see "Hints")
  
  Examples:
  - check_auth using decarator:
  ```python
  from jwt_auth_client.auth_jwt import requires_auth_jwt
  class Protected(AbstractView):
    """Entry point: protected (for test purposes)"""

    @requires_auth_jwt
    def get(self):
        """Return accepted 200 or unauthorized depends on provided
        Bearer token in Authorization header
        """
        return {'message': 'accepted'}, 200
   ```
  
  - get_auth to obtain identity information:
  ```python
    from jwt_auth_client.auth_jwt import get_auth
  	class Protected(AbstractView):
    """Entry point: protected (for test purposes)"""
	    def get(self):
	        """Return accepted 200 or unauthorized depends on provided
	        Bearer token in Authorization header
	        """
	        auth = request.headers.get('Authorization')
		  	if len(auth.split()) == 2:
	    		token = auth.split()[1]
	      	print(token)
	      	print(get_auth(token), type(get_auth(token)))
	        return {'message': 'accepted'}, 200
   ```  
