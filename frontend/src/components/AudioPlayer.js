import React, { useEffect, useRef, forwardRef, useImperativeHandle } from 'react';

const AudioPlayer = forwardRef(({ audio }, ref) => {
  const audioRef = useRef(null);
  useImperativeHandle(ref, () => ({
    stop: () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0; 
      }
    },
  }));

  useEffect(() => {
    const playAudio = async () => {
      if (audioRef.current) {
        try {
          audioRef.current.volume = 0.5; 
          await audioRef.current.play();
        } catch (error) {
          console.error('Error playing audio:', error);
        }
      }
    };

    playAudio();

    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.currentTime = 0; 
      }
    };
  }, [audio]);

  return (
    <div>
      <audio ref={audioRef} src={audio} loop />
    </div>
  );
});

export default AudioPlayer;
