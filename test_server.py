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
def test_other_get_200_ok():
    response = req.get('http://127.0.0.1:5000/cow?msg=something')
    assert response.status_code == 200

def test_get_cow_400_bad():
    response = req.get('http://127.0.0.1:5000/cow')
    assert response.status_code == 400

def test_get_without_keyword_bad():
    response = req.get('http://127.0.0.1:5000/cow?who=dat&wat=do')
    assert response.status_code == 400

# !!!neet to fix
def test_post_not_valid_bad():
    response = req.post('http://127.0.0.1:5000/cow?msg=text')
    assert response.status_code == 405


def test_post_valid_good():
    response = req.post('http://127.0.0.1:5000/cow msg=text')
    assert response.status_code == 201

def test_post_cow_bad():
    response = req.post('http://127.0.0.1:5000/cow')
    assert response.status_code == 400

def test_post_cow_bad():
    response = req.post('http://127.0.0.1:5000/cow who=this how=why')
    assert response.status_code == 400

def test_notPost_rightsyntax_bad():
    response = req.get('http://127.0.0.1:5000/cow msg=texterfe')
    assert response.status_code == 405

def test_any_404_bad():
    response = req.get('http://127.0.0.1:5000/doesntexist_scott_has_a_dog')
    assert response.status_code == 404

def test_any_404_bad2():
    response = req.post('http://127.0.0.1:5000/doesntexist_scott_has_a_dog')
    assert response.status_code == 404
