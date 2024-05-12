import { Header } from '@/components/Header';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`w-full h-full`}>
      <Header></Header>
      {children}
    </div>
  );
}
