function PageWrapper({ children }) {
    return (
      <div className="animate-fadeInUp">
        {children}
      </div>
    );
  }
  
  export default PageWrapper;
  