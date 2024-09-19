import { defineStore } from 'pinia';
import { getDetailUser, updateUser } from '@/services/userApi';
import { ErrorMessage } from '@/models/MessageNotifyModel';


export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    email: '',
    avatar: ''
  }),
  actions: {
    async fetchUser() {
      getDetailUser()
        .then(response => {
          const { username, mail, avatar } = response.data;
          this.username = username;
          this.email = mail;
          this.avatar = avatar;
        })
        .catch(error => {
          ErrorMessage(error);
        });
    },
    updateUserInfo(newInfo) {
      updateUser(newInfo)
        .then(response => {
          const { username } = response.data;
          this.username = username;
        })
        .catch(error => {
          ErrorMessage(error);
        });
    }
  },
  getters: {
    getUser() {
      return {
        username: this.username,
        email: this.email
      };
    }
  }
});
