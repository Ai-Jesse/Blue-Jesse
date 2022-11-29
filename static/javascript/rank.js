/* ajax of leaderboard
call rank() when loads to leaderboard to get the rank */
function rank(){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const user_rank = JSON.parse(this.response);
            for (const user of user_rank) {
                let rank = document.getElementById('rank');
                rank.innerHTML += "<b>" + user['username'] + "</b>: " + user["highest_point"] + "<br/>";
            }
        }
    };
    request.open("GET", "/rank");
    request.send();
}