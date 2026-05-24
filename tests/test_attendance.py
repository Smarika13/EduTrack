def test_mark_attendance_no_token(client):
    response = client.post("/api/v1/attendance",
                           json={
                               "date": "2024-01-15T10:00:00",
                               "status": "present",
                               "student_id": 1,
                               "subject_id": 1
                           })
    assert response.status_code == 401


def test_mark_attendance_as_student(client, admin_user):
    response = client.post("/api/v1/register",
                           json={
                               "roll_no": "nce079bct036",
                               "semester": 5,
                               "dob": "2000-10-12",
                               "name": "Pramisha",
                               "email": "pramisha123@gmail.com",
                               "phone": "9876543210",
                               "faculty": "BCT",
                               "password": "Pramisha@123#"
                           })
    response = client.post("/api/v1/login",
                           json={"email": "pramisha123@gmail.com",
                                 "password": "Pramisha@123#"})
    student_token = response.json()["access_token"]

    response = client.post("/api/v1/attendance",
                           json={
                               "date": "2024-01-15T10:00:00",
                               "status": "present",
                               "student_id": 1,
                               "subject_id": 1
                           },
                           headers={"Authorization": f"Bearer {student_token}"})
    assert response.status_code == 403


def test_mark_attendance_success(client, admin_user):
    # Login as admin
    response = client.post("/api/v1/login",
                           json={"email": admin_user["email"],
                                 "password": admin_user["password"]})
    admin_token = response.json()["access_token"]

    # Create teacher
    response = client.post("/api/v1/admin/teacher",
                           json={
                               "name": "Test Teacher",
                               "email": "teacher@test.com",
                               "phone": "9800000001",
                               "faculty": "BCT",
                               "password": "Teacher@123",
                               "department": "Computer",
                               "qualification": "Masters"
                           },
                           headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    teacher_id = response.json()["id"]

    # Create subject
    response = client.post("/api/v1/subject",
                           json={
                               "name": "Computer Networks",
                               "credit_hr": 3,
                               "faculty": "BCT",
                               "semester": 5,
                               "teacher_id": teacher_id
                           },
                           headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    subject_id = response.json()["id"]

    # Register student
    response = client.post("/api/v1/register",
                           json={
                               "roll_no": "nce079bct036",
                               "semester": 5,
                               "dob": "2000-10-12",
                               "name": "Pramisha",
                               "email": "pramisha123@gmail.com",
                               "phone": "9876543210",
                               "faculty": "BCT",
                               "password": "Pramisha@123#"
                           })
    assert response.status_code == 200
    student_id = response.json()["id"]

    # Login as teacher
    response = client.post("/api/v1/login",
                           json={"email": "teacher@test.com",
                                 "password": "Teacher@123"})
    teacher_token = response.json()["access_token"]

    # Mark attendance
    response = client.post("/api/v1/attendance",
                           json={
                               "date": "2024-01-15T10:00:00",
                               "status": "present",
                               "student_id": student_id,
                               "subject_id": subject_id
                           },
                           headers={"Authorization": f"Bearer {teacher_token}"})
    assert response.status_code == 200
