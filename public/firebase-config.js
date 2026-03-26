// Firebase configuration for tmv-orders
const firebaseConfig = {
  apiKey: "AIzaSyCucxnWxvha6mWsNuqpbn9KqBFkL8mSEZY",
  authDomain: "tmv-orders.firebaseapp.com",
  databaseURL: "https://tmv-orders-default-rtdb.firebaseio.com",
  projectId: "tmv-orders",
  storageBucket: "tmv-orders.firebasestorage.app",
  messagingSenderId: "654674925439",
  appId: "1:654674925439:web:38919d8bded4f954992c4a"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();