document.addEventListener("DOMContentLoaded", () => {
    // Connect to the SocketIO server.
    var socket = io();
  
    // Join a room using the current user's ID.
    // For simplicity, assume a global variable currentUserID is set in a template.
    if (typeof currentUserID !== "undefined") {
      socket.emit('join', {room: currentUserID});
    }
  
    // Listen for progress updates.
    socket.on('progress_update', function(data) {
      // data should contain photo_id and progress (0 to 1)
      let bar = document.getElementById("bar-" + data.photo_id);
      if (bar) {
        bar.style.width = (data.progress * 100) + "%";
      }
    });
  });
  