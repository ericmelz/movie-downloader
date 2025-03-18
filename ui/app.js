const app = Vue.createApp({
    data() {
        return {
            pin: '',
            loading: false
        }
    },
    methods: {
        updatePin(event) {
            this.pin = event.target.value;
        },
        async download() {
            this.loading = true;
            console.log('pin is ' + this.pin)
            const response = await fetch('http://localhost:8000/generate', {method: 'POST'});
            if (!response.ok) throw new Error('Failed to download [Initiation failed]');
            console.log('Successfully initiated download');
            const {report_id} = await response.json();
            console.log("Report ID: ", report_id);

            var time = 0;
            const checkStatus = setInterval(async () => {
                const statusResponse = await fetch('http://localhost:8000/' + report_id + '/status');
                if (statusResponse.ok) {
                    const statusData = await statusResponse.json();
                    if (statusData.ready) {
                        clearInterval(checkStatus);
                        window.open('http://localhost:8000' + statusData.url);
                        console.log('Successfully downloaded');
                        this.loading = false;
                        return;
                    }
                } else {
                    clearInterval(checkStatus);
                    this.loading = false;
                    throw new Error('Failed to download [status check failed]');
                }
                time += 1000;
                if (time > 10000) {
                    this.loading = false;
                    throw new Error("Timeout!!");
                }
            }, 1000);
        }
    }
});
app.mount('#events');
