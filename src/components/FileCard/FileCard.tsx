import React from 'react';
import Cropper, { type ReactCropperElement } from 'react-cropper';
import { FileWithPath } from 'react-dropzone';
import { Icons } from '@/assets/Icons';
import { FaLink, FaRegFilePdf } from 'react-icons/fa6';
import { ImageCustom } from '../ImageCustom/ImageCustom';
import { Dialog, DialogContent, DialogTrigger } from '../ui/dialog';
import { Button } from '../ui/button';

type FileWithPreview = FileWithPath & {
  preview: string;
};
interface FileCardProps {
  i?: number | null;
  file: FileWithPreview;
  files: FileWithPreview[] | null;
  setFiles: React.Dispatch<React.SetStateAction<FileWithPreview[] | null>>;
}

export default function FileCard({ i, file, files, setFiles }: FileCardProps) {
  const [isOpen, setIsOpen] = React.useState(false);
  const [cropData, setCropData] = React.useState<string | null>(null);
  const cropperRef = React.useRef<ReactCropperElement>(null);

  const onCrop = React.useCallback(() => {
    if (!files || !cropperRef.current) return;

    const croppedCanvas = cropperRef.current?.cropper.getCroppedCanvas();
    setCropData(croppedCanvas.toDataURL());

    croppedCanvas.toBlob((blob) => {
      if (!blob) {
        console.error('Blob creation failed');
        return;
      }
      const croppedImage = new File([blob], file.name, {
        type: file.type,
        lastModified: Date.now(),
      });

      const croppedFileWithPathAndPreview = Object.assign(croppedImage, {
        preview: URL.createObjectURL(croppedImage),
        path: file.name,
      }) satisfies FileWithPreview;

      const newFiles = files.map((subFile, j) =>
        j === i ? croppedFileWithPathAndPreview : subFile
      );
      setFiles(newFiles);
    });
  }, [file.name, file.type, files, i, setFiles]);

  React.useEffect(() => {
    function handleKeydown(e: KeyboardEvent) {
      if (e.key === 'Enter') {
        onCrop();
        setIsOpen(false);
      }
    }
    document.addEventListener('keydown', handleKeydown);
    return () => document.removeEventListener('keydown', handleKeydown);
  }, [onCrop]);

  console.log(file);
  console.log(file?.preview ? 'exits' : 'image');
  return (
    <div className="w-fit flex flex-row items-center justify-center gap-2">
      <div className="w-full flex flex-row items-center gap-2">
        {file?.url?.endsWith('.pdf') || file.path!.endsWith('.pdf') ? (
          <FaRegFilePdf fill="secondary" />
        ) : (
          <ImageCustom
            src={cropData ? cropData : file?.preview || file?.url}
            alt={file.name}
            className="h-12 w-12 shrink-0 rounded-md"
          />
        )}

        <div className="flex flex-col">
          <p className="line-clamp-1 text-sm font-medium text-muted-foreground">
            {file.name}
          </p>
        </div>
      </div>
      <div className="">
        {file?.url ? (
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="h-7 w-7"
            onClick={() => {
              window.open(file.url, '_blank');
            }}
          >
            <FaLink />
          </Button>
        ) : file?.preview ? (
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="h-7 w-7"
            onClick={() => {
              window.open(file.preview, '_blank');
            }}
          >
            <FaLink fill="secondary" />
          </Button>
        ) : null}
      </div>
    </div>
  );
}
