const app = Vue.createApp({
    data () {
        return {
            pin: ''
        }
    },
    methods: {
        updatePin(event) {
            this.pin = event.target.value;
        },
        download() {
            console.log('pin is ' + this.pin)
        }
    }
});
app.mount('#events');
