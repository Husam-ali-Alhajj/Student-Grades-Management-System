from managers import UserManager
from auth import AuthManager

def run_first_time_flow_test_v5():
    print("\n========== FIRST TIME USER FLOW TEST V5 ==========\n")

    user_manager = UserManager()
    auth = AuthManager()

    print("🧪 STEP 1: Admin creates raw users")
    user_manager.create_user(
        email="edge_stud_v5@test.com",
        name="Edge Student V5",
        password="EdgeV5#StudTemp",
        role="Student",
        is_active=True,
        is_complete=False
    )

    user_manager.create_user(
        email="edge_teach_v5@test.com",
        name="Edge Teacher V5",
        password="EdgeV5#TeachTemp",
        role="Teacher",
        is_active=True,
        is_complete=False
    )
    print("✔ Raw users created")

    print("\n🧪 STEP 2: Get last created users")
    users = user_manager.get_all_users()
    student_user = users[-2]
    teacher_user = users[-1]

    print("✔ Student user_id:", student_user.user_id)
    print("✔ Teacher user_id:", teacher_user.user_id)

    print("\n🧪 STEP 3: Try wrong password (should fail)")
    bad_login = auth.login(student_user.user_id, "WrongPassword123")
    print("Wrong password login result:", bad_login)

    print("\n🧪 STEP 4: First login with temp passwords")
    stud_session = auth.login(student_user.user_id, "EdgeV5#StudTemp")
    teach_session = auth.login(teacher_user.user_id, "EdgeV5#TeachTemp")

    print("✔ Student session:", stud_session)
    print("✔ Teacher session:", teach_session)

    print("\n🧪 STEP 5: Complete profiles")
    auth.first_login(
        stud_session,
        username="edge_stud_v5_unique",
        name="Edge Student Final",
        email="edge_stud_final_v5@test.com",
        password="EdgeV5#StudFinal"
    )

    auth.first_login(
        teach_session,
        username="edge_teach_v5_unique",
        name="Edge Teacher Final",
        email="edge_teach_final_v5@test.com",
        password="EdgeV5#TeachFinal"
    )
    print("✔ Profiles completed")

    print("\n🧪 STEP 6: Logout both users")
    auth.logout(stud_session)
    auth.logout(teach_session)

    print("Student logged after logout:", auth.is_logged_in(stud_session))
    print("Teacher logged after logout:", auth.is_logged_in(teach_session))

    print("\n🧪 STEP 7: Normal login after profile completion")
    stud_session_2 = auth.login("edge_stud_v5_unique", "EdgeV5#StudFinal")
    teach_session_2 = auth.login("edge_teach_v5_unique", "EdgeV5#TeachFinal")

    print("✔ Student new session:", stud_session_2)
    print("✔ Teacher new session:", teach_session_2)

    print("\n🧪 STEP 8: is_logged_in checks")
    print("Student logged:", auth.is_logged_in(stud_session_2))
    print("Teacher logged:", auth.is_logged_in(teach_session_2))
    print("Fake session logged:", auth.is_logged_in("not-a-real-session"))

    print("\n🧪 STEP 9: Change password + re-login")
    auth.change_password("EdgeV5#StudChanged", stud_session_2)
    auth.logout(stud_session_2)

    relogin = auth.login("edge_stud_v5_unique", "EdgeV5#StudChanged")
    print("✔ Student logged after password change:", relogin)

    print("\n========== TEST V5 COMPLETED SUCCESSFULLY ==========\n")


if __name__ == "__main__":
    run_first_time_flow_test_v5()
