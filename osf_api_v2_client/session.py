import six
import requests

from osf_api_v2_client.utils import(DotDictify,
                                    dotdictify_generator,
                                    file_generator,
                                    get_response_or_exception)

class Session(object):
    def __init__(self, root_url='https://staging2.osf.io/api/v2/', auth=None):
        self.root_url = root_url
        self.auth = auth  # TODO is it okay to have auth be None?

    def get_root(self):
        """
        :return: a DotDictify object of the api root as designated by self.root_url
        """
        response = get_response_or_exception('get', self.root_url)
        response_json = response.json()
        return DotDictify(response_json)

    # USER ACTIONS

    # TODO maybe: get_generator; get_object -- e.g. if I wanted to get a registration...
    # but, if you're passing in the URL you maybe might as well be using the API itself

    # TODO: if a parameter gets passed in, I should process it.
    # TODO: requests -- query parameters = ...

    # TODO: modify DotDictify object, then push it to server to edit it?
    def get_user_generator(self, num_requested=-1):
        """
        :param num_requested: a positive integer or -1; -1 will cause all users
        to be returned; otherwise num_requested number of users will be returned
        :return: a generator containing users
        """
        # TODO consider case when generator is empty?
        target_url = '{}users/'.format(self.root_url)
        # TODO try/except something here? (e.g. raising exceptions for permissions errors?)
        return dotdictify_generator(target_url, auth=self.auth, num_requested=num_requested)

    def get_user(self, user_id):
        """
        :param user_id: 5-character user id
        :return: the user identified by user_id
        """
        url = '{}users/{}/'.format(self.root_url, user_id)
        response = get_response_or_exception('get', url, auth=self.auth)
        data = response.json()[u'data']
        return DotDictify(data)

    # NODE ACTIONS

    def get_node_generator(self, num_requested=-1):
        """
        :param num_requested: a positive integer or -1; -1 will cause all nodes
        to be returned; otherwise num_requested number of nodes will be returned
        :return: a generator containing nodes
        """
        # TODO consider case when generator is empty?
        target_url = '{}nodes/'.format(self.root_url)
        # TODO try/except something here? (e.g. raising exceptions for permissions errors?)
        return dotdictify_generator(target_url, auth=self.auth, num_requested=num_requested)

    def get_node(self, node_id=''):
        """
        If node_id is None, return a generator containing nodes
        If node_id is a valid id, return the node with that id
        If node_id is not a valid node id, raise exception
        :param node_id: 5-character id for a node that can be viewed by this session's auth
        :return: the node identified by node_id
        """
        url = '{}nodes/{}/'.format(self.root_url, node_id)
        response = get_response_or_exception('get', url, auth=self.auth)
        data = response.json()[u'data']
        return DotDictify(data)

    def create_node(self, title="", description="", category="", public="True"):
        """
        :param title: required, string
        :param description: optional, string
        :param category: optional, choice of '', 'project', 'hypothesis', 'methods and measures', 'procedure',
        'instrumentation', 'data', 'analysis', 'communication', 'other'
        :return: created node
        """
        params = {'title': title, 'description': description, 'category': category, 'public': public}
        node = requests.post('{}nodes/'.format(self.root_url), json=params, auth=self.auth)
        return node

    def edit_node(self, node_id, **kwargs):
        # Example kwargs: title='', description='', category='' TODO tags? public?
        # TODO how should this functionality work in terms of when a category is passed in or not?
        # TODO figure out how to change the private setting to public and vice versa
        params = {}  # 'node_id': node_id}
        for key, value in kwargs.items():
            params[key] = value
        print(params)
        response = requests.patch('{}nodes/{}/'.format(self.root_url, node_id),
                                  json=params,
                                  # TODO should use json=params or data=params ?
                                  auth=self.auth
                                  )
        return response

    def delete_node(self, node_id):
        """
        :param node_id: 5-character node id
        :return: none
        """
        response = requests.delete('{}nodes/{}/'.format(self.root_url, node_id), auth=self.auth)
        return response

    # FILE ACTIONS

    # TODO possible to do something like node.get_files_generator() ? ...
    def get_file_generator(self, node_id, num_requested=-1):
        """
        :param node_id: 5-character node id
        :param num_requested: a positive integer or -1; -1 will cause all files
        to be returned; otherwise num_requested number of files will be returned
        :return: a generator containing files related to node_id
        """
        node = self.get_node(node_id)
        files_url = node.links.files.related
        return file_generator(files_url, auth=self.auth)
