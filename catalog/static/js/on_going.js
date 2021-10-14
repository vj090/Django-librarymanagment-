function ask_user(question, yes, no) {
    if (confirm(question)) yes();
    else no()
}

function funYes() {
    alert("Function yes !!!");
}

function funNo() {
    alert("Function No ???");
}

ask_user("You want to confirm", funYes, funNo)