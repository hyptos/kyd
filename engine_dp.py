#!/usr/bin/env python

import os
import dropbox
import tempfile
import provider
from pprint import pformat
from execo import Timer
from execo_engine import Engine, sweep, ParamSweeper, igeom, slugify, logger
import requests


class DropboxBench(Engine):
    """  """

    def create_file(self, size):
        """ """
        fd, fname = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as fout:
            fout.write(os.urandom(size))
        return fname

    def upload_file_sdk(self, client, filePath, fileName):
        """Upload a file's content.
        Args:
            service: Drive API service instance.
            filePath : Path to the file you want to upload.
            fileName : Name of the new file in the drive.
        """
        f = open(filePath, 'rb')
        response = client.put_file(fileName, f)
        return response

    def download_file_sdk(self, client, fileName, filePath):
        """Download a file's content.
        Args:
            client: Dropbox client instance.
            fileName: Name of the file you want to download.
            filePath: Name of the new local file.
        """
        f, _ = client.get_file_and_metadata(fileName)
        out = open(filePath, 'wb')
        out.write(f.read())
        out.close()
        return True


    def getNewToken(self):
        """ Get a new token for a new app """
        p = provider.Provider('dropbox')
        print 'test de connexion a ' + p.provider_name
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(p.app_key, p.app_secret)
        r = requests.get(flow.start())
        if r.status_code == 200:
            print "url:", flow.start()
            print "Please authorize in the browser. After you're done, press enter."
            auth_code = raw_input().strip()
            access_token, user_id = flow.finish(auth_code)
            config = ConfigParser.ConfigParser()
            config.readfp(open('conf.ini'))
            config.set('dropbox', 'token', access_token)
        else:
            return False
        return True

    def init(self):
        """Init the connexion to Dropbox.

        Returns:
        The Dropbox client.
        """
        p = provider.Provider('dropbox')
        if not p.token:
            self.getNewToken()
        return dropbox.client.DropboxClient(p.token)



    def run(self):
        """ """
        p = provider.Provider('dropbox')
        client = dropbox.client.DropboxClient(p.token)
        parameters = {'size': igeom(128, 2048, 5),
                      'db_if': ['rest', 'sdk']}
        combs = sweep(parameters)
        sweeper = ParamSweeper(self.result_dir + '/sweeps', combs)

        f = open(self.result_dir + '/results.txt', 'w')
        f.write("timer_start\t\tsize\tupload_time\tdownload_time\n")
        while len(sweeper.get_remaining()) > 0:
            comb = sweeper.get_next()

            logger.info('Treating combination %s', pformat(comb))
            comb_dir = self.result_dir + '/' + slugify(comb)
            try:
                os.mkdir(comb_dir)
            except:
                pass

            fname = self.create_file(comb['size'])

            timer = Timer()

            if comb['db_if'] == 'sdk':
                self.upload_file_sdk(client, fname, fname.split('/')[-1])
                up_time = timer.elapsed()
                self.download_file_sdk(client, fname.split('/')[-1],
                                       comb_dir + '/' + fname.split('/')[-1])
                dl_time = timer.elapsed() - up_time

                # delete le fichier chez Dropbox
                client.file_delete(fname.split('/')[-1])

                sweeper.done(comb)
            elif comb['db_if'] == 'rest':
                logger.warning('REST interface not implemented')
                sweeper.skip(comb)
                continue
            os.remove(fname)
            f.write("%f\t%i\t%f\t%f\n" % (timer.start_date(), comb['size'],
                                        up_time, dl_time))
        f.close()

if __name__ == "__main__":
    e = DropboxBench()
    e.start()