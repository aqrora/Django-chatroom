const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
      messages: [],
      newMessage: '',
    },
    created() {
      this.loadMessages();
      setInterval(this.loadMessages, 5000);
    },
    methods: {
      loadMessages() {
        axios.get('/api/messages/')
          .then(response => {
            this.messages = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      },
      sendMessage() {
        axios.post('/api/messages/', {
          text: this.newMessage
        })
          .then(response => {
            this.messages.push(response.data);
            this.newMessage = '';
          })
          .catch(error => {
            console.log(error);
          });
      }
    }
  });