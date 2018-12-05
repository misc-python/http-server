import requests as req
# from cowpy import cow

# test get 200
def test_get_200_ok():
    response = req.get('http://127.0.0.1:5000')
    assert response.status_code == 200

# test !GET /: 400 Bad Request
def test_other_get_400_ok():
    response = req.post('http://127.0.0.1:5000')
    assert response.status_code == 400


# GET /cow?msg=text: 200 OK <Text Response>
# def test_get_cow_ok_with_content():

# test !GET /: 400 Bad Request
def test_other_get_400_ok():
    response = req.post('http://127.0.0.1:5000/cow?msg=something')
    assert response.status_code == 400
