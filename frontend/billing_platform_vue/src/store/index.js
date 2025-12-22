import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null
  },
  
  mutations: {
    SET_AUTH(state, { token, user }) {
      state.token = token
      state.user = user
      localStorage.setItem('token', token)
      localStorage.setItem('user', JSON.stringify(user))
    },
    
    LOGOUT(state) {
      state.token = null
      state.user = null
      localStorage.clear()
    }
  },
  
  getters: {
    isLoggedIn: state => !!state.token,
    isAdmin: state => state.user?.is_admin || false,
    currentUser: state => state.user
  }
})