import type { Metadata } from 'next';
import { Montserrat } from 'next/font/google';
import { Header } from '@/components/Header';

export default function Layout({ children }: { children: React.ReactNode }) {
  // await mustBeRole();
  // const session = await getSession();
  return <div className={`w-full h-full`}>{children}</div>;
}
