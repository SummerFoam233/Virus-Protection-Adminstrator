$(() => {
    let user = $.cookie("user");
    if (user != null) {
      user = JSON.parse(user);
      if (user.admin === 0) {
        $("#LiInsert")
          .remove()
      }
    }
    else if(user == null){
      $("#LiInsert")
          .remove()
    }
  })