import Vue from 'vue';
import App from './App.vue';
import './styles/index.css';

SYNO.namespace('SYNO.SDS.App.TestPackage1');

SYNO.SDS.App.TestPackage1.Instance = Vue.extend({
    components: { App },
    template: '<App/>',
});
