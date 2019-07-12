import json
import socket
import config

def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True
    
    
def getDomain(domain):
   if domain == '':
      return 0
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      sql = "SELECT `domain_id` FROM `recorder_domain` WHERE `name` = %s LIMIT 1"
      try:
        cursor1.execute(sql, domain)
      except:
        print('err')
        return 0
      try:
         row = cursor1.fetchone()
         if row == None:
            add = "INSERT INTO `recorder_domain` ( `name`) VALUES ( %s) "
            cursor1.execute(add, domain)
            config.rds_db.commit()
            return cursor1.lastrowid
         else:
            return row['domain_id']
      except:
        print('err')
        return 0
   return 0

def getIP(ip):
   if ip == '':
      return 0
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      sql = "SELECT `ip_id` FROM `recorder_ip` WHERE `address` = %s "
      cursor1.execute(sql, ip)

      while True:
         row = cursor1.fetchone()
         if row == None:

            add = "INSERT INTO `recorder_ip` ( `address`) VALUES ( %s) "
            cursor1.execute(add, ip)
            config.rds_db.commit()
            return cursor1.lastrowid
         else:
            return row["ip_id"]
   return 0

def addFetch(ip, toolkey_id, record_type, records_added, node):

   submit_ip_id = None
   if ip != "":
       submit_ip_id = getIP(ip)
       
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      add = "INSERT INTO `recorder_fetch` ( `toolkey_id`, `record_type`, `records_added`, `reported_on`, `submit_ip_id`, `node` ) VALUES ( %s, %s, %s, NOW(), %s, %s) "
      cursor1.execute(add, [toolkey_id, record_type, records_added, submit_ip_id, node])
      config.rds_db.commit()
      return cursor1.lastrowid
   return 0

def addLookup(domain_id, ip_id, toolkey_id):

   if domain_id == 0 or ip_id == 0 or domain_id == None or ip_id == None:
      print("err addLookup fails")
      return 0
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      sql = "SELECT `pdns_id` FROM `recorder_pdns` WHERE `domain_id` = %s and `ip_id` = %s and `toolkey_id` = %s "
      cursor1.execute(sql, [domain_id, ip_id, toolkey_id])

      while True:
         row = cursor1.fetchone()
         if row == None:
            add = "INSERT INTO `recorder_pdns` ( `domain_id`, `ip_id`, `toolkey_id`, `created`, `last_seen` ) VALUES ( %s, %s, %s, NOW(), NOW()) "
            cursor1.execute(add, [domain_id, ip_id, toolkey_id])
            #print ("  creating lookup " + str(domain_id) + " -> " + str(ip_id))
            config.rds_db.commit()
            return cursor1.lastrowid
         else:
            sql = "UPDATE `recorder_pdns` set `last_seen` = NOW() where `pdns_id` = %s"
            #print (sql)
            cursor1.execute(sql, row["pdns_id"])
            config.rds_db.commit()
            return row["pdns_id"]
   return 0

def addLookupCname(domain_id, domain2_id, toolkey_id):

   if domain_id == 0 or domain2_id == 0 or domain_id == None or domain2_id == None:
      print("err addLookup fails")
      return 0
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      sql = "SELECT `cname_id` FROM `recorder_pdns_cname` WHERE `domain_id` = %s and `domain2_id` = %s and `toolkey_id` = %s "
      cursor1.execute(sql, [domain_id, domain2_id, toolkey_id])

      while True:
         row = cursor1.fetchone()
         if row == None:
            add = "INSERT INTO `recorder_pdns_cname` ( `domain_id`, `domain2_id`, `toolkey_id`, `created`, `last_seen` ) VALUES ( %s, %s, %s, NOW(), NOW()) "
            cursor1.execute(add, [domain_id, domain2_id, toolkey_id])
            #print ("  creating lookup " + str(domain_id) + " -> " + str(domain2_id))
            config.rds_db.commit()
            return cursor1.lastrowid
         else:
            sql = "UPDATE `recorder_pdns_cname` set `last_seen` = NOW() where `cname_id` = %s"
            cursor1.execute(sql, row["cname_id"])
            config.rds_db.commit()
            return row["cname_id"]
   return 0


def addSeen(domain_id, toolkey_id):

   if domain_id == 0 or domain_id == None:
      print("err addLookup fails")
      return 0
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      sql = "SELECT `seen_id` FROM `recorder_pdns_seen` WHERE `domain_id` = %s and `toolkey_id` = %s "
      cursor1.execute(sql, [domain_id, toolkey_id])

      while True:
         row = cursor1.fetchone()
         if row == None:
            add = "INSERT INTO `recorder_pdns_seen` ( `domain_id`, `toolkey_id`, `created`, `last_seen` ) VALUES ( %s, %s, NOW(), NOW()) "
            cursor1.execute(add, [domain_id, toolkey_id])
            config.rds_db.commit()
            return cursor1.lastrowid
         else:
            sql = "UPDATE `recorder_pdns_seen` set `last_seen` = NOW() where `seen_id` = %s"
            cursor1.execute(sql, row["seen_id"])
            config.rds_db.commit()
            return row["seen_id"]
   return 0


def addFlow(ip_id, toolkey_id, bytes_out):

   if ip_id == 0 or ip_id == None or bytes_out == 0:
      print("err addLookup fails")
      return 0
   with config.rds_db.cursor() as cursor1:
      # Read a single record
            add = "INSERT INTO `recorder_flow` (`ip_id`, `bytes_out`, `toolkey_id`, `created` ) VALUES ( %s, %s, %s, NOW()) "
            cursor1.execute(add, [ ip_id, bytes_out, toolkey_id])
            config.rds_db.commit()
            return cursor1.lastrowid

def getAuth(toolkey):
 
   with config.rds_db.cursor() as cursor1:
      # Read a single record
      sql = "SELECT local_id FROM `Auth` WHERE `toolkey` = %s"
      #print(sql)
      try:
        cursor1.execute(sql, toolkey)
      except:
        print('err')
        return 0
      try:
         row = cursor1.fetchone()
         if row == None:
            return 0
         #print (row['count(*)'])
         return row['local_id']
      except:
        print('err')
        return 0
   return 0
   
   
def parsePDNS(json_item, toolkey_id):
    
    if toolkey_id > 0:
       pdns = json.loads(json_item)
       #print (pdns)
       for domain in pdns:
           #print (domain)
           added = 0;
           domain_id = getDomain(domain)
           #print (domain_id)
           ips = pdns[domain]
           for ip in ips:
               if is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip):
                  #print (domain + "=" + ip)
                  ip_id = getIP(ip)
                  if domain_id > 0 and ip_id > 0:
                     addLookup(domain_id, ip_id, toolkey_id)
                     added = 1
                  elif domain_id > 0 and added == 0:
                      addSeen(domain_id, toolkey_id)
               else:
                  #print (domain + ">" + ip)
                  domain2_id = getDomain(ip)
                  if domain_id > 0 and domain2_id > 0:
                     addLookupCname(domain_id, domain2_id, toolkey_id)
                     added = 1
                  elif domain_id > 0 and added == 0:
                      #print ("seen")
                      addSeen(domain_id, toolkey_id)
       return len(pdns)


def parseFlow(json_item, toolkey_id):
    if toolkey_id > 0:
       flow = json.loads(json_item)
       #print (flow)
       for ip in flow:
           #print (ip)
           if is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip):
               ip_id = getIP(ip)
               if ip_id > 0:
                   addFlow(ip_id, toolkey_id, flow[ip])
       return len(flow)


def lambda_handler(event, context):
    
    #print(event)
    #print(context)
    count = 0
    toolkey_id = 0
    job = ""
    
    submit_ip = None
    try:
       submit_ip = event['headers']['X-Forwarded-For']
    except:
       None
    
    node = None
    try:
       node = event['queryStringParameters']['node']
    except:
       None

    try:
        if event['queryStringParameters']['toolkey']:
            #print ("checking toolkey")
            #print(event['queryStringParameters']['toolkey'])
            toolkey_id = getAuth(event['queryStringParameters']['toolkey'])
            record_type = event['queryStringParameters']['feed']
            if toolkey_id > 0 and record_type == "pdns":
               #print("processing json pdns")
               records_added = parsePDNS(event['body'], toolkey_id)
               addFetch(submit_ip, toolkey_id, record_type, records_added, node)
            elif toolkey_id > 0 and record_type == "flow":
               #print("processing json flow")
               records_added = parseFlow(event['body'], toolkey_id)
               addFetch(submit_ip, toolkey_id, record_type, records_added, node)
            else:
               print("authkey not recognized")
    except:
        None
    print ("info: parsed " + str(records_added) + " " + str(record_type) + " records")
    if (toolkey_id == 0):
       return {'statusCode': 403, 'body': "error: access denied for api key provided"}
    elif (records_added == 0):
       return {'statusCode': 204, 'body': "warning: no data received"}
    elif (record_type != "pdns" and record_type != "flow"):
       return {'statusCode': 404, 'body': "error: improper feed type"}
    return {'statusCode': 200, 'body': "info: parsed " + str(records_added) + " " + str(record_type) + " records"}