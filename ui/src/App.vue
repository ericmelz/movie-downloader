<template>
    <v-app-instance class-name="SYNO.SDS.App.TestPackage1.Instance">
        <v-app-window width=850 height=574 ref="appWindow" :resizable="false" syno-id="SYNO.SDS.App.TestPackage1.Window">
            <div class="test-package1-app">
                <div class="title">Hello Test Package1</div>
                <div>
                    <v-button suffix="main" @click="onClick">Documents</v-button>
                    <v-button @click="close">Close</v-button>
                </div>
            </div>
        </v-app-window>
    </v-app-instance>
</template>

<script>
export default {
    data() {
        return {
        };
    },
    methods: {
        onClick() {
            window.open('https://help.synology.com/developer-guide/', '_blank');
        },
        close() {
            this.$refs.appWindow.close();
        },
    },
}
</script>
