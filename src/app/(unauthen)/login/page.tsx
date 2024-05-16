import { Metadata } from 'next';
import React from 'react';
import { getProviders } from 'next-auth/react';
import Login from './Login';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';

export const metadata: Metadata = {
  title: 'Authentication',
  description: 'Authentication forms built using the components.',
};

const LoginPage = async () => {
  return (
    <>
      <div className="p-12 relative h-screen w-full ">
        <ToastContainer />
        <div className="lg:p-8 sm:p-12 ">
          <div className="mx-auto h-full flex w-full flex-col justify-center space-y-6 ">
            <div className="flex flex-col space-y-2 text-center text-primary">
              <h1 className="text-2xl font-semibold tracking-tight">
                Welcome back!
              </h1>
              <p className="text-lg text-muted-foreground">
                Let's build our future together
              </p>
            </div>
            <Login />
          </div>
        </div>
      </div>
    </>
  );
};

export default LoginPage;
