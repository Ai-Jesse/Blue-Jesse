// /* ajax of leaderboard
// call rank() when loads to leaderboard to get the rank */
// function rank(){
//     const request = new XMLHttpRequest();
//     request.onreadystatechange = function () {
//         if (this.readyState === 4 && this.status === 200) {
//             const user_rank = JSON.parse(this.response);
//             let count = 1;
//             for (const user of user_rank) {
//                 let rank = document.getElementById('rank');
//                 rank.innerHTML += "<tr>\r\n<th>" + count + "</th>\r\n<th>" + user['username'] + "</th>\r\n<th>" + user["highest_point"] + "</th>\r\n</tr>";
//                 count = count+1
//             }
//         }
//     };
//     request.open("GET", "/rank");
//     request.send();
// }