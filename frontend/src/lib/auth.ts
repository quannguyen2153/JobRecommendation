'use client';

import jwt from 'jsonwebtoken';
import Cookies from 'js-cookie';

export function isSessionValid() {
  // Get the token from the cookies
  const token = Cookies.get('token');

  if (token) {
    // Decode the token
    const decodedToken = jwt.decode(token);

    // Check if the decodedToken has an 'exp' field
    if (decodedToken && decodedToken.exp) {
      // Get the current time in seconds since the epoch
      const currentTime = Math.floor(Date.now() / 1000);

      // Check if the token has expired
      if (decodedToken.exp < currentTime) {
        // If the token has expired, remove the 'token' and 'user' cookies
        Cookies.remove('token');
        Cookies.remove('user');
        return false;
      } else {
        return true;
      }
    } else {
      // If the token doesn't have an 'exp' field, consider it invalid
      Cookies.remove('token');
      Cookies.remove('user');
      return false;
    }
  } else {
    return false;
  }
}
