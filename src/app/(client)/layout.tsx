import { Header } from '@/components/Header';
import Providers from '@/providers/Providers';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`w-full h-full`}>
      <Providers>
        <Header></Header>
        {children}
      </Providers>
    </div>
  );
}
