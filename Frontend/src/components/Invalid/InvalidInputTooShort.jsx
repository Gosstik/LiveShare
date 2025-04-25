export default function InvalidInputTooShort(props) {
  const { warningStyle } = props;

  return (
    <div className={warningStyle}>
      Comment must contain at least 1 non-whitespace character
    </div>
  );
}
