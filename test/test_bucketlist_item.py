# /test_bucketlist_item.py
"""Tests for bucketlist items
"""
import json
from base import *

class BucketlistItemTestCase(BaseTest):
    """Test cases for bucketlist items
    """
    def test_bucketlist_item_creation(self):
        """Test API can create an bucketlist_item (POST)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result = self.client().post('/bucketlists/1/items',
                                    headers=dict(Authorization="Bearer " + access_token),
                                    data=self.bucketlist_item1)
        self.assertEqual(result.status_code, 201)
        self.assertIn('bucketlist_item1', str(result.data))

    def test_api_return_all_activities(self):
        """Test that the API can return all activities (GET)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result1 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        result2 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item2)
        self.assertEqual(result1.status_code, 201)
        self.assertEqual(result2.status_code, 201)
        result = self.client().get('/bucketlists/1/items',
                                   headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Do stuff', str(result1.data))
        self.assertIn('Do a little more stuff', str(result2.data))

    def test_bucketlist_item_editing(self):
        """Test API can edit an bucketlist_item (PUT)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result1 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        result2 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item2)
        self.assertEqual(result1.status_code, 201)
        self.assertEqual(result2.status_code, 201)
        result = self.client().put(
            '/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={'bucketlist_id':1, 'name':'bucketlist_itemnew', 'description':'New thing'})
        self.assertEqual(result.status_code, 200)
        new_result = self.client().get(
            '/bucketlists/1/items',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('New thing', str(new_result.data))

    def test_bucketlist_item_deleting(self):
        """Test API can delete an bucketlist_item (DELETE)
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        self.create_bucketlist(access_token)
        result1 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        result2 = self.client().post('/bucketlists/1/items',
                                     headers=dict(Authorization="Bearer " + access_token),
                                     data=self.bucketlist_item1)
        self.assertEqual(result1.status_code, 201)
        self.assertEqual(result2.status_code, 201)
        delete_result = self.client().delete(
            '/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(delete_result.status_code, 200)
        #Test for data, should return a 404
        new_result = self.client().get(
            '/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(new_result.status_code, 404)

# make the tests executable
if __name__ == "__main__":
    unittest.main()
