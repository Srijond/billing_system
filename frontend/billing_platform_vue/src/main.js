import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Bootstrap
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css' // If you are using bootstrap-vue
import 'bootstrap/dist/css/bootstrap.min.css'

import 'bootstrap'

Vue.config.productionTip = false

// Global toast helper
Vue.prototype.$toast = function(message, type = 'success') {
  const colors = {
    success: '#28a745',
    error: '#dc3545',
    info: '#17a2b8'
  }
  
  const toast = document.createElement('div')
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 15px 20px;
    background: ${colors[type]};
    color: white;
    border-radius: 5px;
    z-index: 9999;
    max-width: 400px;
    white-space: pre-line;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    animation: slideIn 0.3s;
  `
  toast.innerHTML = message.replace(/\n/g, '<br>')
  document.body.appendChild(toast)
  
  setTimeout(() => {
    toast.style.animation = 'slideOut 0.3s'
    setTimeout(() => toast.remove(), 300)
  }, 5000) // Increased to 5 seconds for error messages
}


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')