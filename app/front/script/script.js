// #region Algemeen
//const IP = prompt('geef publiek IP', 'http://127.0.0.1:5000');
const IP = window.location.hostname + ':5000';
const socket = io.connect(IP);

const init = function () {
    socket.on('connected', function (data) {
        toggleValue = data.value;
        showToggle()
    });
    socket.on('toggle', function (data) {
        console.log(data.value);
        toggleValue = data.value;
        showToggle()
    });
    document.querySelector('.power').addEventListener('click', toggle);
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  init();
});

// #endregion
