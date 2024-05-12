'use client';

import * as React from 'react';

import { cn } from '@/lib/utils';
import { Icons } from '@/assets/Icons';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { signIn } from 'next-auth/react';
import { useForm } from 'react-hook-form';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { AiFillEyeInvisible, AiFillEye } from 'react-icons/ai';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form';
import * as z from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { Loader } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast } from 'react-toastify';
import { setCookie } from 'cookies-next';

const formSchema = z.object({
  email: z.string().min(1, {
    message: 'Email is required',
  }),
  password: z.string().min(1, {
    message: 'Password is required',
  }),
});
const Login = ({ className }: { className?: string }) => {
  const router = useRouter();
  const [isLoading, setIsLoading] = React.useState<boolean>(false);
  const [show, setShow] = React.useState({
    showPass: false,
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const { onLogin } = useAuth();
  async function onSubmit(data) {
    console.log(data);
    setIsLoading(true);
    onLogin(data, (response) => {
      console.log('response:' + response);
      setIsLoading(false);
      if (response.status == 200) {
        const payload = response.data.payload;
        console.log('payload:' + JSON.stringify(payload));
        const token = payload.token;
        // localStorage.setItem('token', token);
        // localStorage.setItem('user', JSON.stringify(payload.data));
        setCookie('token', token);
        setCookie('user', JSON.stringify(payload.data));
        router.push('/');
        toast.success('User login successfully!');
      } else if (response.status == 400) {
        toast.error('Email already exists');
      } else {
        toast.error('Error when login user');
      }
    });
  }
  if (isLoading)
    return (
      <div className="w-full flex flex-col items-center justify-center">
        <Loader />
      </div>
    );
  return (
    <div className="w-full flex flex-col items-center justify-center text-primary">
      <div
        className={cn('grid gap-6 w-[80%] md:w-[70%] lg:w-[60%] ', className)}
      >
        <ToastContainer />
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <div className="grid gap-6">
              <div className="gap-8 flex flex-col">
                <div className="flex flex-col gap-3 ">
                  <Label className="font-bold">Email</Label>
                  <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            className="text-slate-500"
                            placeholder="Please enter your email"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <div className="flex flex-col gap-3 ">
                  <Label className="font-bold">Password</Label>
                  <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                      <FormItem>
                        <FormControl>
                          <Input
                            className="text-slate-500"
                            renderRight={
                              <div
                                onClick={() => {
                                  setShow({
                                    ...show,
                                    showPass: !show.showPass,
                                  });
                                }}
                                className="opacity-50 cursor-pointer hover:opacity-100"
                              >
                                {show.showPass ? (
                                  <AiFillEyeInvisible size={20} />
                                ) : (
                                  <AiFillEye size={20} />
                                )}
                              </div>
                            }
                            value={field.value}
                            onChange={field.onChange}
                            id="password"
                            placeholder="Please enter your password"
                            type={show.showPass ? 'text' : 'password'}
                            autoCapitalize="none"
                            autoComplete="password"
                            autoCorrect="off"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
              </div>

              <Button type="submit">Sign In</Button>
            </div>
          </form>
        </Form>
      </div>

      <p className="mt-10 px-8 text-center text-sm text-muted-foreground">
        Don't have an account?{' '}
        <Link className="font-bold underline text-black" href="/register">
          Sign Up
        </Link>
      </p>
    </div>
  );
};

export default Login;
