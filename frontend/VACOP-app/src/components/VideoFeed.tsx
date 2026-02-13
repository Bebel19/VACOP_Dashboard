import React from 'react';
import './VideoFeed.css';

interface VideoFeedProps {
  title: string;
  streamUrl?: string;
}

const VideoFeed: React.FC<VideoFeedProps> = ({ title, streamUrl }) => {
  return (
    <div className="video-feed-placeholder">
      <h4>{title}</h4>
      <div className="feed-content" style={{ width: '100%', height: '100%', overflow: 'hidden' }}>
        {streamUrl ? (
          <iframe
            src={streamUrl}
            title={title}
            width="100%"
            height="100%"
            scrolling="no"
            style={{ border: 'none', backgroundColor: '#000' }}
            allow="autoplay; fullscreen"
          />
        ) : (
          <p>(En attente du flux vidéo...)</p>
        )}
      </div>
    </div>
  );
};

export default VideoFeed;