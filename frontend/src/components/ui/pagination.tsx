import { Pagination } from '@nextui-org/react';
import React from 'react';
interface PaginationBarProps {
  pageSize: number;
  currentPage: number;
  onPageChange: (page: number) => void;
}
const ProductReviewPaginationBar: React.FC<PaginationBarProps> = ({
  pageSize,
  currentPage,
  onPageChange,
}: PaginationBarProps) => {
  return (
    <div>
      <Pagination
        total={pageSize}
        initialPage={1}
        showControls
        variant="flat"
        isCompact
        showShadow
        boundaries={2}
        page={currentPage}
        onChange={onPageChange}
      ></Pagination>
    </div>
  );
};

export default ProductReviewPaginationBar;
