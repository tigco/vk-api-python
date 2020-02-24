import requests
from requests.exceptions import HTTPError


def get_text_from_wall(params, min_likes = 0):
    """
    Get public posts from a user's or community's wall on VK.com

    Args:
      params: The dictionary containing request parameters. access_token, owner_id (wall owner's id), and v (api version) are required parameters.
      More details here https://vk.com/dev/wall.get
      min_likes: Optional. The minimum number of likes that returned posts have. Default 0.
    Returns:
      The lists containing the texts from the posts or 
    """

    if all (key in params for key in ('access_token', 'owner_id', 'v')) and params['access_token'] and params['owner_id'] and params['v']:
        url = 'https://api.vk.com/method/wall.get'
        try:
            response = requests.get(
                url,
                params,
            )

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            json_response = response.json()['response']
            if json_response['items']:
                return  [item['text'] for item in json_response['items'] 
                            if  'copy_history' not in item.keys() 
                                and 'text' in item.keys() 
                                and item['text'] 
                                and 'likes' in item.keys() 
                                and item['likes']['count'] > min_likes
                        ]
    else:
        print('access_token, owner_id, and v (api version) are required parameters.')
    return 'Error ocurred'


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("access_token", type=str, help="Service access key to use. Must be obtained from VK.com")
    parser.add_argument("owner_id", type=int, help="the user or community ID. Note, community IDs are negative integers. User IDs are positive integers.")
    parser.add_argument("--filter", type=str, default='owner', help="the filter to use. For more details see https://vk.com/dev/wall.get")
    parser.add_argument("--offset", type=int, default=0, help="the offset to use. For more details see https://vk.com/dev/wall.get")
    parser.add_argument("--count", type=int, default=100, help="the count to use. For more details see https://vk.com/dev/wall.get")
    parser.add_argument("--version", type=str, default='5.103', help="the api version to use. For more details see https://vk.com/dev/wall.get")
    parser.add_argument("--min_likes", type=int, default=0, help="the minimum number of likes on returned posts")
    args = parser.parse_args()

    params={
        'access_token': args.access_token,
        'owner_id': args.owner_id,
        'filter': args.filter,
        'offset': args.offset,
        'count': args.count,
        'v': args.version,
    }
    texts = get_text_from_wall(params, args.min_likes)
    if texts and isinstance(texts, list) :
        for text in texts:
            print(text)
            print('\n')
    else: print('The request returned nothing.')
    print('\nALL DONE!')

if __name__ == "__main__":
    main()