# プロジェクト名（仮）

このプロジェクトはdynamic pricingと言う動的に価格を変化させて利益の最大化を目指すシステムです。（あくまで例）

## 開発の手順
1,2,3は最初だけ。
1. **レポジトリをフォークする**

2. **フォークしたリポジトリをクローンする**
    ```bash
    git clone <フォークしたレポジトリのurl>
    ```

3. **オリジナルリポジトリをリモートに追加する**
    ```bash
    cd Hackathon_vol.10
    git remote add upstream https://github.com/situmshr/Hackathon_vol.10
    ```
---------------------------------
4. **作業ブランチを作成する**
    ```bash
    git checkout -b <作業ブランチ名>
    ```

5. **コードを書いてコミット&リモートにプッシュ**
    ```bash
    git add -A
    git commit -m "commitの説明"
    git push origin <作業ブランチ>
    ```

6. **オリジナルリポジトリから最新の変更をフェッチする**
    ```bash
    git fetch upstream
    ```

7. **ローカルの main ブランチを更新する**
    ```bash
    git checkout main
    git merge upstream/main
    ```

8. **作業ブランチに main ブランチの変更をマージする**
    ```bash
    git checkout <作業ブランチ名>
    git merge main
    ```

9. **コンフリクトを解決する**</br>
コンフリクトが発生した場合は手動で解決し、解決後にファイルをステージングし、コミットする。
    ```bash
    git add <コンフリクト解決したファイル>
    git commit -m "Resolved merge conflict with main"
    git push origin <作業ブランチ名>
    ```

10. **プルリクエストを作成する**</br>
GitHub上で、フォークしたリポジトリにアクセスし、プルリクエストする。

11. **誰かがレビューしてマージする**




