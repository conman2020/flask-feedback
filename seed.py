c2 = User(
    username="chocolate",
    password="small",
    email="balllli@msn.com",
    first_name="small",
    last_name="big"
)



CREATE TABLE feedbacks (
        feedback_id SERIAL NOT NULL,
        title VARCHAR(100) NOT NULL,
        content TEXT NOT NULL,
        username VARCHAR(20) NOT NULL,
        PRIMARY KEY (feedback_id),
        FOREIGN KEY(username) REFERENCES users (username)
)


c3 = Feedback(
    title="small",
    content="balllli@msn.com",
    username="gggg"
)
eewfwfg


c4 = Feedback(
    title="small ball",
    content="ball is life",
    username="samfffff"
)


c4 = Feedback(
    title="big ball",
    content="big balls of life",
    username="samfffff"
)