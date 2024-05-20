'use client';
import { Header } from '@/components/Header';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`w-full h-full`}>
      <QueryClientProvider client={queryClient}>
        <Header></Header>
        {children}
      </QueryClientProvider>
    </div>
  );
}
