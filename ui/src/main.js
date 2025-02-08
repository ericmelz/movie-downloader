import Vue from 'vue';
import App from './App.vue';
import './styles/index.css';

SYNO.namespace('SYNO.SDS.App.MovieDownloader');

SYNO.SDS.App.MovieDownloader.Instance = Vue.extend({
    components: { App },
    template: '<App/>',
});
