$(document).ready(function() {
    alert("Actived")
    
    var $messages = $('.messages-content'),
        d, h, m,
        i = 0;
  
    $messages.mCustomScrollbar();
  
    setTimeout(function() {
      fakeMessage();
    }, 100);
    setTimeout(function() {
        fakeMessage();
      }, 100);
    function updateScrollbar() {
      $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
      });
    }
  
    function setDate() {
      d = new Date();
      if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
        $('<div class="checkmark-sent-delivered">&check;</div>').appendTo($('.message:last'));
        $('<div class="checkmark-read">&check;</div>').appendTo($('.message:last'));
      }
    }
  
    function insertMessage() {
      var msg = $('.message-input').val();
      if ($.trim(msg) == '') {
        return false;
      }
      $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      $('.message-input').val(null);
      updateScrollbar();
      setTimeout(function() {
        fakeMessage();
      }, 1000 + (Math.random() * 20) * 100);
    }
  
    $('.message-submit').click(function() {
        alert("wwww");
      insertMessage();
    });
  
    $(window).on('keydown', function(e) {
      if (e.which == 13) {
        insertMessage();
        return false;
      }
    });
  
    var Fake = [
        'Hi there, I\'m Jesse and you?',
        'Nice to meet you',
        'How are you?',
        'Not too bad, thanks',
        'What do you do?',
        'That\'s awesome',
        'Codepen is a nice place to stay',
        'I think you\'re a nice person',
        'Why do you think that?',
        'Can you explain?',
        'Anyway I\'ve gotta go now',
        'It was a pleasure chat with you',
        'Time to make a new codepen',
        'Bye',
        ':)'
      ];
  
    function fakeMessage() {
      if ($('.message-input').val() != '') {
        return false;
      }
      $('<div class="message loading new"><figure class="avatar"><img src="http://askavenue.com/img/17.jpg" /></figure><span></span></div>').appendTo($('.mCSB_container'));
      updateScrollbar();
  
      setTimeout(function() {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="http://askavenue.com/img/17.jpg" /></figure>' + Fake[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
        setDate();
        updateScrollbar();
        i++;
      }, 1000 + (Math.random() * 20) * 100);
    }
  
    $('.button').click(function() {
        $('.menu .items span').toggleClass('active');
        $('.menu .button').toggleClass('active');
      });
  });
  