import urllib,time,datetime,pandas

class Quote(object):
  
  DATE_FMT = '%Y-%m-%d'
  TIME_FMT = '%H:%M:%S'
  
  def __init__(self):
    self.symbol = ''
    header=['Date','Open','High','Low','Close','Volume']
    self.quoteframe=pandas.DataFrame([],columns=header) 
      
  def to_csv(self):
    return ''.join(["{0}  {1}  {2:.2f}  {3:.2f}  {4:.2f}  {5:.2f}  {6:,}\n".format(self.symbol,
              self.quoteframe.Date[bar].strftime('%Y-%m-%d'),
              self.quoteframe.Open[bar],self.quoteframe.High[bar],self.quoteframe.Low[bar],self.quoteframe.Close[bar],self.quoteframe.Volume[bar]) 
              for bar in xrange(len(self.quoteframe))])
                  
  def write_csv(self,filename):
    with open(filename,'w') as f:
      f.write(self.to_csv())
        
  def read_csv(self,filename):
    self.symbol = ''
    self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
    for line in open(filename,'r'):
      symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
      self.symbol = symbol
      dt = datetime.datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
      self.append(dt,open_,high,low,close,volume)
    return True

  def __repr__(self):
    return self.to_csv()

   
class GoogleQuote(Quote):
  ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
  def __init__(self,symbol,start_date,end_date=datetime.date.today().isoformat()):
    super(GoogleQuote,self).__init__()
    self.symbol = symbol.upper()
    start = datetime.date(int(start_date[0:4]),int(start_date[5:7]),int(start_date[8:10]))
    end = datetime.date(int(end_date[0:4]),int(end_date[5:7]),int(end_date[8:10]))
    url_string = "http://www.google.com/finance/historical?q={0}".format(self.symbol)
    url_string += "&startdate={0}&enddate={1}&output=csv".format(
                      start.strftime('%b %d, %Y'),end.strftime('%b %d, %Y'))
    csv = urllib.urlopen(url_string).readlines()
    csv.reverse()
    for bar in xrange(0,len(csv)-1):
      ds,open_,high,low,close,volume = csv[bar].rstrip().split(',')
      open_,high,low,close = [float(x) for x in [open_,high,low,close]]
      volume=int(volume)
      dt = datetime.datetime.strptime(ds,'%d-%b-%y')
      self.quoteframe.loc[bar]=[dt,open_,high,low,close,volume]








#this creats monthy average close price,  can be added into google.py.
def monthly(symbol,start_date,end_date=datetime.date.today().isoformat()):
		quote = GoogleQuote(symbol,start_date,end_date).quoteframe
		month = []  # create an empty list for month
		for bar in xrange(0,len(quote)):
			month.append(str(quote.Date[bar].year) + '-' +
			 str(quote.Date[bar].month).zfill(2))
		quote['Month'] = month
		quoteMonthly = quote.groupby('Month').Close.mean().reset_index().rename(columns={'Close':symbol})
		return quoteMonthly

