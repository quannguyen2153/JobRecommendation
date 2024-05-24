import { Metadata } from 'next';
import React from 'react';
import Register from './Register';
import jwt from 'jsonwebtoken';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';

export const metadata: Metadata = {
  title: 'Authentication',
  description: 'Authentication forms built using the components.',
};

const RegisterPage = async () => {
  return (
    <div className="mx-auto h-full flex w-full flex-col justify-center space-y-6 text-primary items-center">
      <ToastContainer />
      <h1 className="text-2xl font-semibold tracking-tight">Create Account</h1>
      <p className="text-md max-w-[50ch] text-center">
        Join us to start building a new future together
      </p>
      <Register />
    </div>
  );
};

export default RegisterPage;
